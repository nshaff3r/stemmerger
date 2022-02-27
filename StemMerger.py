import os
import sys

# Stem tracks
stack = []


def main():
    print("Please make sure all stem files follow proper format, e.g. NAME_NUMBER.FILETYPE")
    counter = {}  # Dict to ensure four stem files for each song
    for i in range(1, 5, 1):  # Populates dict
        counter[i] = 0
    # Common audio file extensions
    audiotypes = [".aac", ".aiff", ".flac", ".m4a", ".mp3", ".ogg", ".opus", ".wav", ".webm"]

    while True:  # Checks and ensures valid path is given that contains correctly formatted stem files
        try:
            path = input("Path to stem files: ")
            for filename in os.listdir(path):
                if os.path.splitext(filename)[1] not in audiotypes:
                    filename += 1
                counter[int(os.path.splitext(filename)[0][-1])] += 1
                stack.append(str(filename))
            break
        except OSError:  # No valid path
            print(r"Please use a valid path (i.e C:\Users\nshaf\Downloads\Stemfiles).", end='\n\n')
        except ValueError:  # Path has audio files that are incorrectly named
            print("Please use a path that contains only stem files using the proper "
                  "naming format: NAME_NUMBER.FILETYPE.", end='\n\n')
            stack.clear()
        except TypeError:  # Path contains non audio files
            print("Please make sure path only contains audio files.", end='\n\n')

    os.chdir(path)  # Updates directory
    freq = counter[1]  # Number of songs
    res = True
    for num in counter:  # Ensures even number of stem files (four per song)
        if counter[num] != freq:
            res = False
    if res is False:
        sys.exit("An uneven amount of stem files (not four per track) was found.\nThis program was only designed"
                 " to run with four files per track.\nPlease correct this error and rerun the program.")

    current = counter  # Renames dict for keeping track of current songs
    for i in range(freq):
        track = 1  # Track names are indexed at 1
        song = stack[0].split("_")[-2]  # Based on proper formatting, this is where the title is
        for itm in stack:
            if itm.split("_")[-2] == song:  # Stem file for current song is found
                current[track] = itm  # Adds stem file to current song dict
                track += 1
        if len(current) == 4:  # Error check, just in case
            merger(current, song)  # Merges all tracks for current song
        else:
            print(f"An error occurred with {song}.")

        for itm in current:  # Removes tracks from stack since they've been processed
            stack.remove(current[itm])

    # Offers option to convert merged songs
    ans = input_checker(['y', 'n'], "\nWould you like to convert your songs to a different audio format? ")
    if ans == 'y':
        ext = input_checker(audiotypes, "What format? ",
                            errormsg=f"Please use one of the following formats: {audiotypes}")
        for song in os.listdir(path):
            name = os.path.splitext(song)[0]
            if '_' not in name:  # Selects only merged songs
                os.system(f'ffmpeg -i "{song}" -acodec {ext[1:]} "{os.path.splitext(song)[0] + ext}"')
    print("Task finished successfully.")


def merger(stems, output):
    # Runs ffmpeg command to merge stem files
    os.system(f'ffmpeg -i "{stems[1]}" -i "{stems[2]}" -i "{stems[3]}" -i "{stems[4]}"'
              f' -filter_complex amix=inputs=4:duration=first "{output}".wav')


# Recursively checks for correct user input given a list of responses, a prompt,
# and an optional error message. If no error message is provided, the default will be used.
def input_checker(responses, prompt, errormsg="Sorry, I don't recognize your input. Please try again. \n"):
    # Prompts the user for their input and standardizes it
    rawinput = input(prompt).rstrip().lower()

    # Iterates through list of proper responses, returning one if there is a match
    for response in responses:
        if response in rawinput:
            return response

    # Since no match was found, the error message is printed and the function is returned to be rerun
    print(errormsg)
    return input_checker(responses, prompt, errormsg)


if __name__ == "__main__":
    main()
