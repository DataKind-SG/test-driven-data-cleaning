# Driver program
library(stringr)
source("clean_methods.R")

clean_columns <- function(input_file,output_file){

    reader <- file(input_file, open = 'rt')
    writer <- file(output_file, open = 'wt')
    num_col = 0
    
    column_names <- scan(reader,what=character(),nlines=1,sep=',',skip=0,quiet=TRUE)
    num_col = length(column_names)
    column_names <- vapply(column_names,FUN=function(x) 
        if(str_detect(x,',')) paste0('\"',x,'\"') else x,FUN.VALUE=character(1),USE.NAMES=FALSE)
    write(column_names,file=writer,ncolumns=num_col,sep=',')
    
    column_methods = list()
    for (i in 1:num_col) {
        column_methods[i] = paste0("clean_col_",i)
    }
    
    while (length(row <- scan(reader,what=character(),nlines=1,sep=',',skip=0,quiet=TRUE)) > 0 ){
        cleaned_row = character()
        for (i in 1:num_col) {
            cleaned_row[i] = get(column_methods[[i]])(row[i])
            if(str_detect(cleaned_row[i],",")) cleaned_row[i] <- paste0('\"',cleaned_row[i],'\"')
        }
        write(cleaned_row,file=writer,ncolumns=num_col,sep=',')
    }
    
    close(reader)
    close(writer)
}

input_file <- $input_filename
output_file <- $output_filename
clean_columns(input_file,output_file)