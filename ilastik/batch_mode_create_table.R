#####
#batch process and create tables containing lineages longer than 100 frames with tracking results and intensity
#20210520
#author: William
#email: williams8645@gmail.com
#####
setwd('D:/Charite/labA/WP1/Large_scale_image_processing/Mydata') # this directory contains 'Output' folder
library(tidyverse)

field_list = c(1:430)

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
for (i in field_list) {
  field=sprintf('xy%03d',i)
  
  tracking_table=sprintf("Output/%s/%s-t_tracking_table.csv",field,field)
  c2_intensity_table=sprintf("Output/%s/%schannel2intensities_table.csv",field,field)
  c3_intensity_table=sprintf("Output/%s/%schannel3intensities_table.csv",field,field)
  
  trackingfinal_edited <- read.csv(tracking_table, header=TRUE)
  trackingfinal_edited <- subset(trackingfinal_edited, 
                                 select = c(frame, labelimageId, trackId, lineageId, parentTrackId, mergerLabelId, Object_Center_0, Object_Center_1, Center_of_the_object_0, Center_of_the_object_1)) #to select only the columns necessary for lineage tracking
  
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
  ###convert the list into a table
  
  finalListLong=finalList[[1]]%>%mutate(lineage=1)
  for (i in 2:length(finalList)){
    x=finalList[[i]]%>%mutate(lineage=i)
    if (nrow(x)>100) {finalListLong = rbind(finalListLong,x)}
  }    
  write.csv(finalListLong,file=sprintf('longtable/%s_final_table.csv',field),row.names = F)
}

#run batch processing and get all long table


