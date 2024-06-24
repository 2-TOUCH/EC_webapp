const sequelize = require("../database");
const { DataTypes } = require("sequelize");

/* 
This model represents access requests for the incoming Ecocar members. 
The purpose is to capture the requester's first name, last name, email address, 
and the subteam they wish to join.
Additionally, it includes fields to track the approval status by the team lead 
("teamleadapprove") and the IT department ("itapprove"), with default values set
 to "PENDING".
*/
const accessRequest = sequelize.define(
  "EcocarAccessRequests", // Model Name
  {
    firstname: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    lastname: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    emailaddress: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    subteam: {
      type: DataTypes.ENUM(
        "PCM",
        "CAV",
        "SDI",
        "DEI",
        "PM",
        "HMI/UX",
        "Communications",
        "System Safety",
      ),
      allowNull: false,
    },
    teamleadapprove: {
      type: DataTypes.ENUM("PENDING", "APPROVED", "REJECTED"),
      defaultValue: "PENDING",
    },
    itapprove: {
      type: DataTypes.ENUM("PENDING", "APPROVED", "REJECTED"),
      defaultValue: "PENDING",
    },
    isOnboardingSent: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    PhotoWaiverSentID: {
      type: DataTypes.STRING,
      defaultValue: "NOT YET SENT",
      allowNull: false,
    },
    isPhotoWaiverSigned: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    UPASentID: {
      type: DataTypes.STRING,
      defaultValue: "NOT YET SENT",
      allowNull: false,
    },
    isUPASigned: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    isTeamRosterFilled: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    isOnboardingComplete: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    token: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      allowNull: false,
      unique: true,
    },
  },
);

// Synchronize the model with the database (create the table if it doesn't exist)
sequelize.sync()
  .then(() => {
    console.log('\nDatabase: "ecocar" and table: "EcocarAccessRequest" are synced\n');
  })
  .catch((err) => {
    console.error('\nError synchronizing the database:', err);
  });

module.exports = accessRequest;
