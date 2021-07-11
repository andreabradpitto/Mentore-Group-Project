# Mentore-Group-Project 
## Subgroup - Ontology
Our part is to design ontology regarding school subjects. For isstance, we chave chosen Geography, Maths and Physics as a subjects. The hierarchy is modified using existing CARESSES.owl file. 

## Software requirements

* Java 1.8 older version
*	Protégé 5.5
*	Python(version >= 3.6)


## Installing Packages

In order to install some of the packages in Python, run:

```bash
pip install flask
```
```bash
pip install flask_restful
```
(optional)
```bash
pip install re
```


## Instructions

To run ontology and start the conversation , open a terminal, move to the folder(Flask_CARESSES\dialogue_tree), and then run: 

```bash
java -jar new_CKB.jar -nationality Indian  -virtual 1
```

* After running it in the terminal, you’ll get **OK** message(That means owl file is working perfect)

**Note**: Here we choose Nationality **Indian** because, the ontology which we designed have instances linked to Indian(others like English and Japanese are not included, just not to make more complicated)

Now, move to this folder(Flask_Caresses) in the terminal 1, and then run:

```bash
mkdir clients            #Only required for the first time.
```

```bash
python dialogue_manager.py 
```

Also, open another terminal 2(keeping terminal 1 open, as server is running) move to this folder(Flask_CARESSES), and then run:

```bash
python test_dialogue_manager.py 
```

Then robot will start conversation by assigning you a client_id(for instance., 0), you can now develop conversation regarding school subjects.

The triggering keywords that you can direct to particular topic:

* I like school or **school** – questions regarding school subjects
* I like maths or **maths** – questions regarding maths (also, **Probability** also can be used as it is a subtopic of maths)
* I like geography or **geography** – questions regarding geography (also, **Continents** also can be used as it is a subtopic of geography)
* I like physics or **physics** – questions regarding physics (also, **Knimenatics** also can be used as it is a subtopic of physics)

The positive and negative user answers to get a positive and negative replies of the particular topic:

* **"yes", "Yes", "ok", "Ok", "Fine", "sure", "Sure", "Of course", "of course"** – In this case, robot replies with positive sentence.
* **"No", "no"**  – In this case, robot replies with negative sentence.
* Click **ctrl+c** to end the conversation.

(**Note**: When you end the convo and start again, make sure to delete credentials.txt and clients\0  in (Flask_CARESSES) folder, and then follow the same procedure as above **instructions**

## Video Tutorial
A detailed video on Ontology hierarchy can be found at the following link.

[Video]

A video showing how to steup files, run and start the conversation can be found at the following link.

[Video](https://unigeit.sharepoint.com/sites/GP_2RS-Subgroup2/Documenti%20condivisi/Registrazioni/New%20channel%20meeting-20210710_202302-Meeting%20Recording.mp4?web=1)

* The conversation is carried away in the terminal(i.e., using keyboard) as a part of our (**Ontology Subgroup**) work. 
* Whereas, **Protocols Subgroup** uses TTS, STT to have live conversation(i.e., using voice) as it is thier part.  


## Developers

* Aliya Arystanbek - s4842279@studenti.unige.it 
* Chetan Chand Chilakapati - s4850111@studenti.unige.it 
* Daulet Babakhan - s4842280@studenti.unige.it
* Vishruth X - s4848208@studenti.unige.it

