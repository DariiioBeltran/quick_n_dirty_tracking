# **quick_n_dirty_tracking**
This project is intended to easily and quickly design mesocycles and track them through GoogleSheets. One simply creates a yaml file in the `mesocycles` directory (following the format/schema shown in  `mesocycle_template.yaml`) and runs the `setup_mesocycle_sheets` command to create and set up the GoogleSheet to track progress throughout the mesocycle.

At the time of this writing, this project only supports the creation of the GoogleSheets. The next feature will be a command `analyze_mesocycle` which will perform some statistical analysis and give some insights about your progress during this mesocycle. The analysis will be fully automated, will generate some visualizations of your progress and generate a pdf report that we'll upload to your GoogleDrive.

# **Set Up**
1. Clone this repository
2. Enable the GoogleSheets and GoogleDrive apis in the Google Cloud Console
3. Download your credentials from Google and paste them in a file called `credentials.json` in the same directory as the `Justfile`
4. Create a `.env` file with an env variable as follows `GMAIL=youremail@gmail.com`
5. Run `just setup-dev` to install the dependencies
6. You are now ready

# **Commands**
### setup_mesocycle_sheets
After you create a mesocycle yaml file, say we call it `mesocycle_one.yaml`, run the following command to create the associated GoogleSheet:
```
just quick-n-dirty-tracking setup_mesocycle_sheets mesocycle_one ''
```
You will receive an email granting you access to the created sheet. Please keep the format of the data the same since the `analyze_mesocycle` command will rely heavily on the schema of these sheets.

### analyze_mesocycle
Not implemented yet, will update this part of the documentation once it's complete.
