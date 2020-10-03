## Setup db
## Setup image processing
## Setup bluetooth coms

## Wait for cow to get onto the scale
    ## If register mode:
        ## Position cow.
            ## Use app to signal to take a picture and do health check:
                #send cow data to front and go idle
    ## Else if active:
        ## When scale feels like there is a cow on it:
            #Do image processing
                #If know cow:
                    #send cow data to front
    ## Else if idle:
        ## Do nothing
