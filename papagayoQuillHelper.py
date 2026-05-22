import json
import copy
from tkinter import Tk, filedialog

#dict that shows how they will be stored in the frames
mouth_order = {
    "AI": 0,
    "E": 1,
    "O": 2,
    "U": 3,
    "WQ": 4,
    "L": 5,
    "FV": 6,
    "MBP": 7,
    "etc": 8,
    "rest": 9
}



def readPapaOutput(papa_file_path):
    """
    Reads a .dat file produced by Papagayo. Put an example file later.
    """
    with open(papa_file_path, "r") as txt_file:
        phoneme_tuples = []
        lines = txt_file.readlines()
        for line in lines[1:]: #skip first line (should be something like "MohoSwitch1")
            
            line = line.replace("\n", "")
            line = line.split(" ")
            print(line)
            print(line[0])
            #store as frame number, line text (Preston Blair mouth name)
            if(line[0] == "-1"):
                line[0] = "0"
            current_tuple = (int(line[0]), line[1])
            phoneme_tuples.append(current_tuple)

        print(phoneme_tuples)
        return phoneme_tuples
    
def find_mouth(json_data, mouthName):
    """
    recursive search to find the paint layer that matches name provided in the Quill file
    should be exact match to mouth layer name (should provide a default)
    """
    if isinstance(json_data, dict):
        if "Implementation" in json_data:
            for child in json_data["Implementation"].get("Children", []):
                if child.get("Name") == mouthName and child.get("Type") == "Paint":
                    return child
        # keep searching deeper
        for v in json_data.values():
            result = find_mouth(v, mouthName)
            if result:
                return result
    elif isinstance(json_data, list):
        for item in json_data:
            result = find_mouth(item, mouthName)
            if result:
                return result
    return None

def edit_quill_json(json_data, phoneme_tuples, mouth):
    """
    Creates a new layer that has a series of frames based off the original mouth layer and the Papagayo data
    There is no need to re-do the drawings! They essentially serve as the indices for the frames. So you only need the original drawings, no more than 10
    """
    #first, create a new layer by making a copy of mouth and adding to json with a new name? 

    new_mouth = copy.deepcopy(mouth)
    new_mouth["Name"] = "lip-sync-output"

    orig_drawings = mouth["Implementation"]["Drawings"] 
    new_drawings = copy.deepcopy(orig_drawings)
    orig_frames = mouth["Implementation"]["Frames"] 
    
    new_frames = []

    for i in range(len(phoneme_tuples)): #stop on the penultimate one; will have a different process for the very last one (no start/end)
        frame_start = phoneme_tuples[i][0]
        
        phoneme = phoneme_tuples[i][1]
        phoneme_num = int(mouth_order[phoneme]) #use this for both the drawings and the frames info
        
        #first check that it's not the last one, then do this and append more than once!
        if(i == len(phoneme_tuples) -1):
            num_frames = 1
            
        else:
            next_frame = phoneme_tuples[i+1][0] 
            num_frames =  next_frame - frame_start #how many times to repeat this drawing and frame 
        
        #now define the frame from the original frames list
        frame_copy = copy.deepcopy(orig_frames[phoneme_num])
        for f in range(num_frames):
            new_frames.append(frame_copy)
    #set new_mouth's drawings and frames to the new lists
    new_mouth["Implementation"]["Drawings"] = new_drawings
    new_mouth["Implementation"]["Frames"] = new_frames
    #add new_mouth after mouth!!!!

    children = json_data["Sequence"]["RootLayer"]["Implementation"]["Children"]

    mouth_index = children.index(mouth)

    children.insert(mouth_index + 1, new_mouth)


    return json_data




def main():

    # Hide the Tkinter root window
    root = Tk()
    root.withdraw()
    
    opening_message = "Hi! This tool will help automate the process of viseme animation in Quill."
    opening_message+= "\nBefore you start: \n\n1. Have a Papagayo .dat file prepared."
    #opening_message+= "\nSee https://github.com/DanielSWolf/papagayo-lip-sync for more info."
    opening_message+= "\n\n. You should also have a Quill project prepared. It should have a single Mouth paint layer that contains the 10 basic mouth shapes in order, one per frame, as seen in the example project."
    opening_message+= "\n\n. The order is as follows: AI, E, O, U, WQ, L, FV, MBP, etc, rest. Maintaining this order is very important!"
    opening_message+= "\n\n. Make a back-up copy of your orignal Quill project! This tool will modify Quill.json."
    print(opening_message)
    print()
    input("Press enter to start!")

    # Ask for the Quill json file
    print("\nSelect the json file from your Quill project.")
    quill_json = filedialog.askopenfilename(
        title="Select the Quill.json file from your Quill project",
        filetypes=[("JSON files", "Quill.json")]
    )
    if not quill_json:
        print("No file selected. Exiting.")
        return

    # Load JSON
    with open(quill_json, "r") as f:
        data = json.load(f)
        
    #Ask for Papagayo .dat file
    print("\nSelect the .dat file Papagayo generated.")
    papa_dat = filedialog.askopenfilename(
        title="Select the .dat Papagayo file",
        filetypes=[(".dat files", "*.dat")]
    )
    if not papa_dat:
        print("No .dat file selected. Exiting.")
        return
    
    #read the papagayo output (if it exists)
    phoneme_tuples = readPapaOutput(papa_dat)

    mouth = input("\nPlease type the name of the paint layer (capitalization matters!) that includes the ordered, 10 mouthshapes. If you leave this blank, it will default to PapagayoMouth.\n")
    if mouth == "":
        mouth = "PapagayoMouth"
    #Edit the Quill json file
    mouth = find_mouth(data, mouth)
    edit_quill_json(data, phoneme_tuples, mouth)
        
    # Save over the original Quill.json file
    output_path = quill_json
    # Save JSON
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully modified Quill project. Please try opening in Quill.")

if __name__ == "__main__":
    main()
