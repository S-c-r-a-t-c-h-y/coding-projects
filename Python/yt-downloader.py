from pytube import YouTube

url = input("Enter The Link Of The Video: ")
print("The Link Is : " + url)



yt = YouTube(url)

title =  yt.title
print("The Title Of The Video Is : " + title )

print(f"The Views Of The Video Is : {yt.views}")

print(f"The Lenght Of The Video Is : {yt.length}")

print(f"The Channel Who Post The Video Is : {yt.rating}")

print("The Description Of The Video Is : " + yt.description)





while True:
	YN = str(input("Are You Sure You Want To Install The Video ? (yes / no)\n"))
	
	if YN.lower() == "yes" :
	    ys = yt.streams.get_highest_resolution()
	    print("Downloading.......")
	    ys.download("C:\YT_DOWNLOADS")
	    print("Downlaod Completed!!")
	    
	    break


	elif YN.lower() == "no" :
	    print("No Proplem")
	    
	    break


	else :
	    print("Please Retry Again Because It Is Not yes Or no")
	    