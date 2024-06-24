const express = require("express");
const router = express.Router();
require("dotenv").config();
const teamRosterModel = require("../models/teamRosterModel");
const accessRequestModel = require("../models/accessRequestModel");

/*
Route: POST '/'
Purpose: To receive data about approved members and store their member data 
in the EcocarTeamRosters database table.
Change EcocarAccessquests.isTeamRosterFilled for this member to be true as well
*/
router.post("/", async (req, res) => {
  try {
    // Get fetched data (member data)
    const {
      firstName,
      lastName,
      emailaddress,
      phoneNumber,
      subTeam,
      leaderShipRole,
      degree,
      major,
      classType, // class
      graduationTerm,
      lookEmployment,
      employmentBegins,
      gender,
      raceEthnicity,
      countryCitizenship,
      tShirtSize,
      linkedInURL,
      photoWaiver,
      gm,
    } = req.body;

    console.log(teamRosterModel.tableAttributes);

    // Create row (data) from fetched data and Save into teamRoster table
    const teamRoster = await teamRosterModel.create({
      firstName: firstName,
      lastName: lastName,
      emailAddress: emailaddress,
      phoneNumber: phoneNumber,
      subTeam: subTeam,
      leadershipRole: leaderShipRole,
      degree: degree,
      major: major,
      classType: classType,
      graduationTerm: graduationTerm,
      lookEmployment: lookEmployment,
      employmentBegins: employmentBegins,
      gender: gender,
      raceEthnicity: raceEthnicity,
      countryCitizenship: countryCitizenship,
      tShirtSize: tShirtSize,
      linkedInURL: linkedInURL,
      photoWaiver: photoWaiver,
      gm: gm,
    });

    const accessRequest = await accessRequestModel.findOne({
      where: { emailaddress: emailaddress },
    });

    // Request Not Found on database
    if (!accessRequest) {
      return res
        .status(404)
        .json({ success: false, error: "Access Request Not Found" });
    }
    await accessRequest.update({ isTeamRosterFilled: true });

    console.log(teamRoster);
    return res.status(200).json({
      success: true,
      msg: `Successfully inserted data into EcocarTeamRosters: 
      ${teamRoster.firstName} 
      ${teamRoster.lastName}`,
    });
  } catch (error) {
    console.error(error.message);
    return res.status(500).send({ success: false, error: error.message });
  }
});

/*
Route: GET '/login'
Purpose: To retrieve data needed for user login by querying the team roster 
database.
*/
router.get("/login", async (req, res) => {
  try {
    const lastName = req.query.lastName;
    const firstName = req.query.firstName;

    // Find User from database
    const user = await teamRosterModel.findOne({
      where: {
        lastName: lastName,
        firstName: firstName,
      },
    });

    // Found User
    if (user) {
      return res.status(200).json({ success: true, data: user });
    }
    // User not in database
    else {
      return res.status(404).json({ success: false, message: "No User Found" });
    }
  } catch (error) {
    // Error with the server
    console.log(error.message);
    return res.status(500).json({
      success: false,
      error: `Error with the Server: ${error.message}`,
    });
  }
});

module.exports = router;
