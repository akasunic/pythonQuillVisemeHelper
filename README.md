You can download the .exe file to run the command line application directly. If you run the .exe, you don't need to have Python installed or have any command line experience. 

Please note (as I explain in the app) that you'll have to use Rhubarb Lip Sync from the command line separately to produce the text output you'll use in the Quill Viseme Helper: 
https://github.com/DanielSWolf/rhubarb-lip-sync

**More tips on using Rhubarb BEFORE you use the pythonQuillVisemeHelper**

Full instructions are on Daniel Wolf's github page above, but I'm including a few extra instructions for those new to the command line. To run Rhubarb, note that you'll need to use the Command Prompt:

    1. Type "Command Prompt" on your Windows Search bar and open.
    2. Open the folder where rhubarb.exe is located, and copy the file path. 
    3. Set your directory in the command line to this folder using the command cd (command diretory). 
        Type: cd _your-file-path_. It should look something like this:
        
        cd C:\Users\YourName\OneDrive\Desktop\Rhubarb-Lip-Sync-1.14.0-Windows\Rhubarb-Lip-Sync-1.14.0-Windows
        
    4. Put your audio file in the same folder where rhubarb.exe is OR copy the file path for your audio file.
    5. Run rhubarb using the following command:
    
        rhubarb -o output.txt _name-of-your-file.ogg_ 

Note that you must include the file extension (either .ogg or .txt). If your audio file is stored in a different folder, you must specify the whole path. For example:

    rhubarb -o output.txt C:\Users\Anna\OneDrive\Documents\AudioFiles\someAudioFile.wav

You can name the file something different than output.txt; this is just an example. 

The Rhubarb Lip Sync github page has a lot more information about different options you can use, such as including a transcription file to help with the audio analysis. 

**Running the python script to create viseme animations in Quill**

Now you can use the Rhubarb output (output.txt, or whatever you named it) in the Python script provided here. The easiest option is to download the .exe file, but you can also choose to download and run the .py file if you prefer.

When you download and then double-click the quillVisemeHelper.py file, it will open up a simple command line application. That app includes instructions, so I'm not providing additional guidelines here at this time.

I have not tested this extensively, so please reach out if you are having trouble and I can troubleshoot and/or make modifications! If a Quill template or video instructions would be helpful, please let me know and I can put something simple together. I may eventually create a version that uses Daniel Wolf's Rhubarb silently if there is interest so that you don't have to use a command prompt. 

And if anyone would like me to update this so it can handle Papagayo output as well, please contact me. 
