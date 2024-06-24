const sequelize = require("../database");
const { DataTypes } = require("sequelize");

/*
This model is designed to manage and organize diverse information about team 
members participating in the Ecocar project. It captures details including 
first name, last name, email address, phone number, subteam affiliation, 
leadership role, educational background, graduation status, 
employment preferences, gender, ethnicity, citizenship, t-shirt size, 
LinkedIn profile URL, and other relevant data.
*/
const teamRoster = sequelize.define(
  "EcocarTeamRosters", // Model Name
  {
    firstName: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    lastName: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    emailAddress: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        isEmail: {
          msg: "Invalid email address",
        },
      },
    },
    phoneNumber: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    subTeam: {
      type: DataTypes.ENUM(
        "PCM",
        "SDI",
        "CAV",
        "PM",
        "System Safety",
        "HMI/UX",
        "Communications",
        "DEI",
        "n/a (faculty)",
      ),
      allowNull: false,
    },
    leadershipRole: {
      type: DataTypes.ENUM(
        "None (team member only)",
        "None",
        "Technical Specialist",
        "CAVs GRA",
        "PCM GRA",
        "DEIM",
        "PM",
        "SDI Subteam Leader",
        "CAVs Subteam Leader",
        "PCM Subteam Leader",
        "HMI Subteam Leader",
        "CM",
        "Other",
        "n/a (faculty)",
      ),
      allowNull: false,
    },
    degree: {
      type: DataTypes.ENUM(
        "Associates",
        "Bachelors",
        "Masters",
        "Doctorate",
        "n/a (faculty)",
        "Other",
      ),
      allowNull: false,
    },
    major: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    classType: {
      type: DataTypes.ENUM(
        "Freshman",
        "Sophomore",
        "Junior",
        "Senior",
        "5th Year",
        "Graduate Student",
        "Faculty",
      ),
      allowNull: false,
    },
    graduationTerm: {
      type: DataTypes.ENUM(
        "Fall 2022",
        "Spring 2023",
        "Summer 2023",
        "Fall 2023",
        "Spring 2024",
        "Summer 2024",
        "Fall 2024",
        "Spring 2025 or later",
        "n/a (faculty)",
      ),
      allowNull: false,
    },
    lookEmployment: {
      type: DataTypes.ENUM(
        "Yes: Full-Time",
        "Yes: Internship",
        "Yes: Co-op",
        "Yes: Internship or Co-op",
        "No",
      ),
      allowNull: false,
    },
    employmentBegins: {
      type: DataTypes.ENUM(
        "ASAP",
        "Winter 2022",
        "Summer 2023",
        "Fall 2023",
        "Winter 2023",
        "Summer 2024",
        "Fall 2024",
        "n/a",
      ),
      allowNull: false,
    },
    gender: {
      type: DataTypes.ENUM(
        "Female",
        "Male",
        "Non-binary",
        "Prefer not to say",
      ),
      allowNull: false,
      defaultValue: "Prefer not to say",
    },
    raceEthnicity: {
      type: DataTypes.ENUM(
        "Asian",
        "Black",
        "Hispanic",
        "Middle Eastern",
        "Multi-Racial",
        "Native American",
        "Other",
        "Pacific Islander",
        "Prefer Not to Answer",
        "White",
      ),
      allowNull: false,
    },
    countryCitizenship: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    tShirtSize: {
      type: DataTypes.ENUM(
        "Male XS",
        "Male S",
        "Male M",
        "Male L",
        "Male XL",
        "Male 2XL",
        "Male 3XL",
        "Male 4XL",
        "Female XS",
        "Female S",
        "Female M",
        "Female L",
        "Female XL",
        "Female 2XL",
        "Female 3XL",
        "Female 4XL",
      ),
      allowNull: false,
    },
    linkedInURL: {
      type: DataTypes.STRING,
      defaultValue: "",
    },
    photoWaiver: {
      type: DataTypes.STRING,
      defaultValue: "",
    },
    gm: {
      type: DataTypes.STRING,
      defaultValue: "",
    },
  },
);

// Synchronize the model with the database (create the table if it doesn't exist)
sequelize.sync()
  .then(() => {
    console.log('\nDatabase: "ecocar" and table: "EcocarTeamRosters" are synced\n');
  })
  .catch((err) => {
    console.error('\nError synchronizing the database:', err);
  });

module.exports = teamRoster;
