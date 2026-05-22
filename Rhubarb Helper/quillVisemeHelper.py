import json
from tkinter import Tk, filedialog

timeConversion = 12600; #factor to convert from seconds to Quill 'time'

def readRhubarbOutput(rhu_file_path):
    with open(rhu_file_path, "r") as txt_file:
        vis_tuples = []
        lines = txt_file.readlines()
        for line in lines:
            
            line = line.replace("\n", "")
            line = line.split("\t")
            #convert to proper time (from seconds to Quill units)
            current_tuple = (float(line[0])*timeConversion, line[1])
            vis_tuples.append(current_tuple)

        #print(vis_tuples)
        return vis_tuples
    
def find_mouth(json_data, mouthName):
    """
    recursive search to find the mouth top level folder in the Quill file
    """
    if isinstance(json_data, dict):
        if "Implementation" in json_data:
            for child in json_data["Implementation"].get("Children", []):
                if child.get("Name") == mouthName:
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

def edit_quill_json(json_data, vis_tuples, mouth):
    """
    Goes through children of mouth, matches up with output from rhubarb that has
    been cleaned into viseme tuples of time and letter, and determines
    when to make visible/invisible in Quill.
    """

    children = mouth.get("Implementation", {}).get("Children", [])
    for i in range(len(vis_tuples)):
        letter = vis_tuples[i][1].lower()
        time = vis_tuples[i][0]
        for c in children:
            if i==0:
                if c.get("Name").lower != letter:
                    visibility = c["Animation"]["Keys"]["Visibility"]
                    visibility.append({
                        "Time": 0,
                        "Value": False,
                        "Interpolation": "None"
                    })
            if c.get("Name").lower() == letter:
                visibility = c["Animation"]["Keys"]["Visibility"]
                visibility.append({
                    "Time": time,
                    "Value": True,
                    "Interpolation": "None"
                })
                if i<len(vis_tuples)-1:#if it's not the very last one, then see when to turn it off
             
                    next_time = vis_tuples[i+1][0]
                    visibility = c["Animation"]["Keys"]["Visibility"]
                    visibility.append({
                        "Time": next_time,
                        "Value": False,
                        "Interpolation": "None"
                    })
    return json_data




def main():

    # Hide the Tkinter root window
    root = Tk()
    root.withdraw()
    
    opening_message = "Hi! This tool will help automate the process of viseme animation in Quill."
    opening_message+= "\nBefore you start: \n\n1. Run Rhubarb Lip Sync on a .wav or .ogg file. Follow the command line instructions. It will output a .txt file."
    opening_message+= "\nSee https://github.com/DanielSWolf/rhubarb-lip-sync for more info."
    opening_message+= "\n\n2. You should also have a Quill project prepared. It should have a Mouth folder that contains either single paint layers or folders entitled A, B, C, D, E, F, G, H, X (see Rhubarb Lip Sync documentation for viseme examples)."
    opening_message+= "\n\n3. Make a back-up copy of your orignal Quill project! This tool will modify Quill.json."
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
        
    #Ask for Rhubarb txt file
    print("\nSelect the .txt file outputted from Rhubarb Lip Sync.")
    rhubarb_txt = filedialog.askopenfilename(
        title="Select the .txt file outputted from Rhubarb Lip Sync",
        filetypes=[("Text files", "*.txt")]
    )
    if not rhubarb_txt:
        print("No Rhubarb file selected. Exiting.")
        return
    
    #read the rhubarb output (if it exists)
    vis_tuples = readRhubarbOutput(rhubarb_txt)

    mouth = input("\nPlease type the name of your top level mouth folder. If you leave blank, it will default to Mouth.")
    if mouth == "":
        mouth = "Mouth"
    #Edit the Quill json file
    mouth = find_mouth(data, mouth)
    edit_quill_json(data, vis_tuples, mouth)
        
    # Save over the original Quill.json file
    output_path = quill_json
    # Save JSON
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully modified Quill project. Please try opening in Quill.")

if __name__ == "__main__":
    main()