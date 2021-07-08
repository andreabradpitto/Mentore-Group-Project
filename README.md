# Mentore-Group-Project ONTOLOGY  readme

This is the readme for the branch devoted to the **Mentore** **Ontology** development.

## :exclamation: Software requirements

* Java 1.8 older version
*	Protégé 5.5
*	Python(version >= 3.6)


## :white_check_mark: Software installation

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


## :information_source: Instructions

To run ontology and start the conversation , open a terminal, move to the folder(Flask_Caresses\dialogue_tree), and then run: 

```bash
java -jar new_CKB.jar -nationality Indian  -virtual 1
```

* After running it in the terminal, you’ll get **OK** message(That means owl file is working perfect)
* Note: Here we choose Nationality **Indian** because, the ontology which we designed have instances linked to Indian(others like English and Japanese are not included, just to not make more complicated)

Now, move to this folder(Flask_Caresses) in the terminal 1, and then run:

```bash
python dialogue_manager.py 
```

Also, open another terminal 2(keeping terminal 1 open, as server is running) move to this folder(Flask_Caresses), and then run:

```bash
python test_dialogue_manager.py 
```

Then robot will start conversation by assigning you a client_id(for instance., 0), you can now develop conversation regarding school subjects.

The triggering keywords that you can direct to particular topic:

* I like school or **school** – questions regarding school subjects
* I like maths or **maths** -- questions regarding maths (also, PROBABLITY also can be used as it is a subtopic of maths)
* I like geography or **geography** -- questions regarding geography (also, CONTINENTS also can be used as it is a subtopic of geography)
* I like physics or **physics** -- questions regarding physics (also, KINEMATICS also can be used as it is a subtopic of physics)
* Click **ctrl+c** to end the conversation.

(Note: When you end the convo and start again, make sure to delete credentials.txt and clients\0 folder, and then follow the same procedure as above)

## 📰 Additional information
A small video is attached here just for an idea of how to run.(soon to be done)
VIDEO





**Mentore** has been coded with Ubuntu 20.04, but it has also been tested on Windows 10, and no issues were found.  

The window size of **Mentore** is set by default to 800×480, in order to match the screen resolution of the robot used in the overall project, *A Motivational And Entertaining Ontology-based Robotic System For Education*.  

Head over to the [doc folder](https://github.com/andreabradpitto/Mentore-Group-Project/tree/GUI/doc) to check the [Group Project Proposal](https://github.com/andreabradpitto/Mentore-Group-Project/tree/GUI/doc/Group%20Project%20proposal.docx), the [papers](https://github.com/andreabradpitto/Mentore-Group-Project/tree/GUI/doc/papers) on which our work is based, and some other useful resources.  
  
For a list of features that are planned in future releases, please check **Mentore**'s Help page [dedicated section](https://github.com/andreabradpitto/Mentore-Group-Project/blob/GUI/guide/help.md#features-that-will-be-supported-in-the-future).

## :suspect: Developers

Andrea Pitto - s3942710@studenti.unige.it  
Syed Muhammad Raza Rizvi - s4853521@studenti.unige.it  
Laiba Zahid - s4853477@studenti.unige.it

