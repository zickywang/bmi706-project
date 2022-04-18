# bmi706-2022-ps3

Hello, Ziqi!


## Requirements

Please make sure to have the following downloaded and installed on your machine before proceeding.

- [Visual Studio Code](https://code.visualstudio.com/download)
- [Git](https://git-scm.com/download)
- [Anaconda](https://docs.anaconda.com/anaconda/install/)

> If you have a preferred text editor and/or know how to manage python virtual environments, please view these requirements
as recommendations.

### Getting started

#### Create **private** GitHub repo from `hms-dbmi/bmi706-2022-ps3`

In order to work independently of your classmates, we ask that you create a **private GitHub repository** for this template repo.
Select the **Download ZIP** option to download the archive for this folder.

<img width="1024" src="https://user-images.githubusercontent.com/24403730/162062582-25a89e2f-0ec2-4b2f-8c87-2f39462d0046.png">

Unzip the archive and drag the folder into VS Code. Within VS Code, select the **Source Control** and **Publish to GitHub**.
Modify the name in the prompt at the top of the editor to `bmi706-2022-ps3`, and select **Publish to GitHub Private repository**.

<img width="1024" src="https://user-images.githubusercontent.com/24403730/162064726-a3126988-9763-48cb-af13-af7c7d1ac1a5.png">

This will create a private GitHub repository under `<YOUR-GITHUB-USERNAME>/bmi706-2022-ps3`. This step is essential for eventually
sharing your application on Streamlit Cloud.

#### Making changes

You can now open your initialized project in VS Code and begin editing.

<img width="1024" src="https://user-images.githubusercontent.com/24403730/162005639-febd095b-268c-4650-ab9e-6f88c5c252ad.png">

Selecting a file from the sidebar will open the file in the editor where you are free make changes.

#### Committing changes

A *commit* is a snapshot of the state of your repository at a specific time. Git keeps track of history of
your repository via commits so that you can revert back to a prior version at any time. In order to
synchronize your local changes with the fork on GitHub, you will need to create a *new commit* 
adding the changes you've made. 

Let's practice making a commit by replacing "Hello, world" with "Hello, `<your name>`" at the top of this file.

- Open `README.md` in VS Code.

<img width="1024" src="https://user-images.githubusercontent.com/24403730/162011100-fa0bfa15-001d-43bf-aa7a-ce6fd406e58a.png">

- Replace `world` at the top of the file with *your name* and save the file.

<img width="1024" src="https://user-images.githubusercontent.com/24403730/162011310-65828f46-b4a1-4d35-a74d-6aa2c54f260b.png">

> Note how the file tab for `README.md` is now yellow with an "M", signifing that it has been modified. The **Source Control** icon in the 
> sidebar additionally has shows a `1`, indicating that `1` file has changed.

- Click the **Source Control** icon in the sidebar and enter *Message* describing the changes we've made. Click the 
"Commit" check mark to stage and commit our changes.

<img width="1024" src="https://user-images.githubusercontent.com/24403730/162014900-e4d99a32-390a-4259-a56d-5f6e5e8d65fb.png">

- Click the Synchronize Changes to update GitHub with our latest changes

<img width="1024" src="https://user-images.githubusercontent.com/24403730/162014837-42f21bf3-bc97-4e56-bdca-bec6d3af9828.png">


### Developing with `streamlit`

You'll need to set up a Python environment for working your Streamlit application locally. Streamlit's only officially-supported environment
manager on Windows, macOS, and linux is [Anaconda Navigator](https://docs.anaconda.com/anaconda/navigator/). Please make sure you 
have this installed. (The following is adapted from Streamlit's [documentation](https://docs.streamlit.io/library/get-started/installation).)

#### Create a new Python environment with Streamlit

1.) Follow the steps provided by Anaconda to
[set up and manage your environment](https://docs.anaconda.com/anaconda/navigator/getting-started/#managing-environments) 
using the Anaconda Navigator.

2.) Select the "▶" icon next to your new environment. Then select "Open terminal":

<img width="1024" src="https://i.stack.imgur.com/EiiFc.png">


3.) In the terminal that appears, type:

```bash
pip install streamlit
```

4.) Test that the installation worked:

```bash
streamlit hello
```

Streamlit's Hello app should appear in a new tab in your web browser.


#### Use your new environment

1.) In Anaconda Navigator, open a terminal in your environment (see step 2 above).

2.) In the terminal that appears, navigate to your local workspace and run:

```bash
streamlit run streamlit_app.py
```

This will open the template streamlit app in the web browser. You can now start editing the contents
of `streamlit_app.py`, and refresh the page in your web browser we see changes.
