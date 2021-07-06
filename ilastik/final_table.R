#creating date: April.28.2021
#author: Huai-Yu William Liou (refer to lineages_corrected by Shivani)
#email: williams8645@gmail.com
############################################################################
setwd(dirname(rstudioapi::getSourceEditorContext()$path))
setwd('../')
library(tidyverse)
library(ggpubr)
library(plotly)
library(ggrepel)

field='xy002'

tracking_table=sprintf("Output/%s/%s-t_tracking_table.csv",field,field)
c2_intensity_table=sprintf("Output/%s/%schannel2intensities_table.csv",field,field)
c3_intensity_table=sprintf("Output/%s/%schannel3intensities_table.csv",field,field)

trackingfinal_edited <- read.csv(tracking_table, header=TRUE)
trackingfinal_edited <- subset(trackingfinal_edited, 
                               select = c(frame, labelimageId, trackId, lineageId, 
                                          parentTrackId, mergerLabelId, Object_Center_0, 
                                          Object_Center_1, Center_of_the_object_0, 
                                          Center_of_the_object_1, Size_in_pixels_0)) #to select only the columns necessary for lineage tracking

###create a merge table

channel2_edited <- read.csv(c2_intensity_table, header=TRUE) 
channel3_edited <- read.csv(c3_intensity_table, header=TRUE) 

channel2_edited=channel2_edited%>%
  mutate(xcenter = as.integer(Center.of.the.object_0), 
         ycenter = as.integer(Center.of.the.object_1))%>%
  rename(Mean.Intensity.c2=Mean.Intensity)%>%
  rename(frame=timestep)
channel3_edited=channel3_edited%>%
  mutate(xcenter = as.integer(Center.of.the.object_0), 
         ycenter = as.integer(Center.of.the.object_1))%>%
  rename(Mean.Intensity.c3=Mean.Intensity)%>%
  rename(frame=timestep)
trackingfinal_edited=trackingfinal_edited%>%
  mutate(xcenter = round(Center_of_the_object_0), 
         ycenter = round(Center_of_the_object_1))
merge_table=trackingfinal_edited%>%
  left_join(select(channel2_edited,c("xcenter","ycenter","frame","Mean.Intensity.c2","Center.of.the.object_0","Center.of.the.object_1")),
                      by=c("xcenter","ycenter","frame"))%>%
  left_join(select(channel3_edited,c("xcenter","ycenter","frame","Mean.Intensity.c3","Center.of.the.object_0","Center.of.the.object_1")),
            by=c("xcenter","ycenter","frame"))


###generate cell trajectories from the head of lineages
#this function create lineages in one family (lineageId)
create_lineage = function() {
  lineageList=list()
  lineageList[[1]]=currentlin%>%
    filter(frame==min(currentlin$frame))%>%
    mutate(lineageTrackId = 0, divisionTimes = 0) #lineageTrackId is based on division times
  for (i in (min(currentlin$frame)+1):max(currentlin$frame)) {  #iterate from the first frame to the last
    currentframe=currentlin%>%filter(frame==i)
    currentframe=currentframe[order(currentframe$parentTrackId),]
    c=1
    for (j in currentframe$trackId) {
      temprow=filter(currentframe,trackId==j)
      pTId=temprow$parentTrackId
      if (pTId == 0) {     #no division, use trackId to search
        k=1
        while (TRUE) {     #search for the right df by its trackId on the last row
          y=tail(lineageList[[k]],1)
          if (j == y$trackId){    #?sometimes joining tracking and intensity table duplicate data in tracking table, makes trackId not unique
            temprow=mutate(temprow, lineageTrackId = y$lineageTrackId, divisionTimes = y$divisionTimes)
            lineageList[[k]]=rbind(lineageList[[k]],temprow)
            break
          }
          k=k+1
        }
      }
      else {    #division happens, use parentTrackId to search
        k=1
        while (TRUE) {     #search for the right df by its trackId on the last row
          y=tail(lineageList[[k]],1)
          if (pTId == y$trackId){
            if (c==1){
              lineageList[[(length(lineageList)+1)]]=lineageList[[k]]
              temprow=mutate(temprow, lineageTrackId = y$lineageTrackId+(1/2**(y$divisionTimes+1)), divisionTimes = y$divisionTimes+1)
              lineageList[[k]]=rbind(lineageList[[k]],temprow)
              c=c+1
              break
            }
            else {
              temprow=mutate(temprow, lineageTrackId = y$lineageTrackId-(1/2**(y$divisionTimes+1)), divisionTimes = y$divisionTimes+1)
              lineageList[[k]]=rbind(lineageList[[k]],temprow)
              c=1
              break
            }
          }
          k=k+1
        }
      }
    }
  }
  return(lineageList)
}


finalList=list()
linindex = sort(unique(merge_table$lineageId))
for (l in linindex){
  currentlin=filter(merge_table,lineageId==l)
  if (l==-1){  #if the currentlin contains false detection, save to the finalList and continue the next loop
    finalList[[1]]=currentlin
    next
  }
  if (nrow(currentlin)<100) {  #discard the short lineages (family), you may want to disable this line to get all lineages
    next
  }
  lineageList = create_lineage()   #create lineages
  for (i in 1:length(lineageList)){   #store into finalList
    finalList[[(length(finalList)+1)]]=lineageList[[i]]
  }
}



#make a copy of finalList in case you need
finalList_copy=finalList
finalList=finalList_copy


finalList=finalList[lapply(finalList,nrow)>0]

###convert the list into a table

finalListLong=finalList[[1]]%>%mutate(lineage=1)
for (i in 2:length(finalList)){
  x=finalList[[i]]%>%mutate(lineage=i)
  if (nrow(x)>100) {finalListLong = rbind(finalListLong,x)}
}    
write.csv(finalListLong,file=sprintf('longtable/%s_final_table.csv',field),row.names = F)

###plots
finalListLong = read.csv(sprintf('longtable/%s_final_table.csv',field), header=TRUE)

#histogram
N=c()
lineage=c()
frame=c()
lineage_index = sort(unique(finalListLong$lineage))
for (i in lineage_index) {
  a=finalListLong[finalListLong$lineage == i,]
  if (a$lineageId[1]==-1) next
  lineage=c(lineage,i)
  N=c(N,nrow(a))
  frame=c(frame,a$frame[1])
}
countdf=data.frame(lineage,N,frame)%>%filter(N<=232)

countdf%>%
  ggplot(aes(x=N))+geom_histogram()+
  theme_classic()+
  theme(text=element_text(size=20))+
  labs(title=sprintf("Field: %s",field),
       subtitle = sprintf("Mean length: %.2f; Total lineages: %d",mean(countdf$N),nrow(countdf)),
       x = 'lineage length')

#rank by the length of lineagId
length_rank = select(finalListLong,lineageId)
length_rank = data.frame(table(length_rank$lineageId))
length_rank = length_rank[order(length_rank$Freq, decreasing = TRUE),]%>%
  rename(lineageId = Var1)%>%
  rename(length = Freq)

plot_list=list()
for (i in length_rank$lineageId[1:5]){
  p = finalListLong%>%
    filter(lineageId==i)%>%
    mutate(Norm.Intensity.c3 = ((Mean.Intensity.c3-min(Mean.Intensity.c3))/(max(Mean.Intensity.c3)-min(Mean.Intensity.c3))))%>%
    mutate(Norm.Intensity.c2 = ((Mean.Intensity.c2-min(Mean.Intensity.c2))/(max(Mean.Intensity.c2)-min(Mean.Intensity.c2))))%>%
    ggplot(aes(x=frame*0.5,y=Norm.Intensity.c3,group = lineage))+geom_line(size = 0.2, color = 'green')+
    geom_line(aes(x=frame*0.5, y = Norm.Intensity.c2, group = lineage), size = 0.2,color = 'red')+
    geom_vline(data=finalListLong%>%filter(lineageId==i)%>%filter(parentTrackId != 0),
               aes(xintercept = frame*0.5),size=0.1)+
    theme_classic()+
    theme(text=element_text(size=5))+
    labs(title=sprintf('%s lineageId %s',field,i),
         x = 'hour',
         y = 'a.u.')
  plot_list[[i]]=p
}

pdf('Rplot.pdf')
ggarrange(plot_list[[1]], plot_list[[2]], plot_list[[3]], plot_list[[4]], plot_list[[5]],
          ncol=1, nrow = 5)
dev.off()

finalListLong%>%
  filter(lineageId == 69)%>%
  mutate(Norm.Intensity.c3 = ((Mean.Intensity.c3-min(Mean.Intensity.c3))/(max(Mean.Intensity.c3)-min(Mean.Intensity.c3))))%>%
  mutate(Norm.Intensity.c2 = ((Mean.Intensity.c2-min(Mean.Intensity.c2))/(max(Mean.Intensity.c2)-min(Mean.Intensity.c2))))%>%
  plot_ly()%>%
  group_by(lineage)%>%
  add_trace(x=~frame*0.5,y=~lineageTrackId,z=~Norm.Intensity.c3, mode='lines', type='scatter3d', name='cell cycle')%>%
  add_trace(x=~frame*0.5,y=~lineageTrackId,z=~Norm.Intensity.c2, mode='lines', type='scatter3d', name='circadian clock')%>%
  add_trace(data=finalListLong%>%filter(lineageId==69)%>%filter(parentTrackId != 0),
              x=~frame*0.5,y=~lineageTrackId,z=0, mode='lines', type='scatter3d', name='division event')

i=7
end_point=finalListLong%>%
  filter(lineageId == i)%>%
  group_by(lineage)%>%
  summarise(lineageTrackId=lineageTrackId[frame == max(frame)],frame=max(frame))
  
  

tree=finalListLong%>%
  filter(lineageId == i)%>%
  ggplot(aes(x=frame*0.5,y=lineageTrackId, group = lineage))+geom_line()+
  geom_label(data=end_point,aes(x=frame*0.5,y=lineageTrackId,label=lineage),size = 3)+
  #geom_point(data=end_point,aes(x = frame*0.5, y = lineageTrackId,color = lineage))+
  theme_classic()+
  theme(text=element_text(size=10))+
  labs(title=sprintf('%s lineageId %s',field,i),
       x = 'hour',
       y = '')
tree


p = finalListLong%>%
  filter(lineageId==i)%>%
  mutate(Norm.Intensity.c3 = ((Mean.Intensity.c3-min(Mean.Intensity.c3))/(max(Mean.Intensity.c3)-min(Mean.Intensity.c3))))%>%
  mutate(Norm.Intensity.c2 = ((Mean.Intensity.c2-min(Mean.Intensity.c2))/(max(Mean.Intensity.c2[frame<120])-min(Mean.Intensity.c2))))%>%
  ggplot(aes(x=frame*0.5,y=Norm.Intensity.c3,group = lineage))+geom_line(size = 0.5, color = 'green')+
  geom_line(aes(x=frame*0.5, y = Norm.Intensity.c2, group = lineage), size = 0.5,color = 'red')+
  geom_vline(data=finalListLong%>%filter(lineageId==i)%>%filter(parentTrackId != 0),
             aes(xintercept = frame*0.5),size=0.1)+
  facet_wrap(~lineage,ncol = 1)+
  ylim(0,1)+
  theme_classic()+
  theme(text=element_text(size=10))+
  labs(title=sprintf('%s lineageId %s',field,i),
       x = 'hour',
       y = 'a.u.')
p

field = c(1:430)
ml=list()
c=0
pdf('R_statistic_analysis.pdf')
for (i in field){
  pos = read.csv(sprintf('longtable/xy%03d_final_table.csv',i), header=TRUE)
  ml[[i]] = pos
  c=c+1
  print(c)
  if (c==20) {
    well = bind_rows(ml)
  m=well%>%
    group_by(lineage)%>%
    summarise(mean = mean(Mean.Intensity.c2))%>%
    ggplot(aes(y=mean))+geom_density()+
    labs(title = sprintf('No.%d',(i/20)))
  print(m)
  c=0
  ml=list()
  }
}
dev.off()

