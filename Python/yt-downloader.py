from pytube import YouTube

url = input("Enter The Link Of The Video: ")
print("The Link Is : " + url)

yt = YouTube(url)

print(f"The Title Of The Video Is : {yt.title}")
print(f"The Views Of The Video Is : {yt.views}")
print(f"The Length Of The Video Is : {yt.length}")
print(f"The Channel Who Post The Video Is : {yt.rating}")
print(f"The Description Of The Video Is : {yt.description}")

while True:

	if (YN := str(input("Are You Sure You Want To Install The Video ? (yes / no)\n")).lower()) == "yes" :
	    ys = yt.streams.get_highest_resolution()
	    print("Downloading.......")
	    ys.download("C:\\YT_DOWNLOADS")
	    print("Download Completed!!")
	    break

	elif YN == "no" :
	    print("No Problem")	    
	    break

	else :
	    print("Invalid input, please try again")
	    