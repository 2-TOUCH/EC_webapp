const express = require("express");
const router = express.Router();
require("dotenv").config();
const accessRequestModel = require("../models/accessRequestModel");
const nodemailer = require("nodemailer");
const { Op } = require("sequelize");

// This module defines various endpoints to handle access requests and approvals

// Function to Send Email to the IT once Requested from the client
const sendAccessRequestMail = async (selectedMemberRowData) => {
  for (const memberRow of selectedMemberRowData) {
    const { firstname, lastname, token, emailaddress } = memberRow;
    console.log("Email sending to: ");
    console.log("token: ", token);
    console.log("firstname: ", firstname);
    console.log("lastname: ", lastname);
    console.log("emailaddress: ", emailaddress)

    // Remember to replace "localhost:5000" with the actual URL in deployment
    const approveLink = `http://localhost:5000/access-requests/approve-by-it?token=${token}`;

    // It utilizes nodemailer to send access request approval emails to the IT department.
    const transporter = nodemailer.createTransport({
      service: "gmail",
      auth: {
        user: process.env.EMAIL_USERNAME,
        pass: process.env.EMAIL_PASSWORD,
      },
    });

    const mailOptions = {
      from: process.env.EMAIL_USERNAME,
      to: process.env.IT_DEPT_EMAIL,
      subject: `[EcoCAR] VPN request for ${firstname} ${lastname}`,
      text: `
        We need VPN approval for the following member:\n
        ${firstname} ${lastname}\n 
        Email Address: ${emailaddress}\n
        \n
        Please click the link below AFTER you have granted VPN access to the member.\n
        Access request database update link: ${approveLink}\n
        This would help us feedback to the database so we know that this student has been given VPN access.\n
      `,
    };
    console.log("Access request email sent to IT Dept!!!");

    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        console.error("Error sending email", error.message);
        throw new Error("Had Error with the nodemailer!!");
      } else {
        console.log("Email sent", info.response);
      }
    });
  }
};

// Retrieve new requests that are pending to be approved to Access Request webpage
router.get("/all", async (req, res) => {
  try {
    const allData = await accessRequestModel.findAll({
      where: {
        [Op.or]: [
          { teamleadapprove: "PENDING" },
          { teamleadapprove: "APPROVED" },
        ],
        itapprove: "PENDING",
      },
    });
    res.json(allData);
    // console.log(allData);
  } catch (error) {
    console.error("Error retrieving data:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Get data from frontend to send access request email with approve link to IT dept.
router.post("/approved-by-teamlead", async (req, res) => {
  try {
    const { selectedMembers } = req.body;
    console.log("selectedMembers: ", selectedMembers);

    const selectedMemberRowData = await accessRequestModel.findAll({
      where: {
        emailaddress: selectedMembers.map((member) => member.emailaddress),
      },
    });
    console.log("selectedMemberRowData: ", selectedMemberRowData);

    // Update teamleadapprove status for each member
    for (const member of selectedMemberRowData) {
      await member.update({ teamleadapprove: "APPROVED" });
    }

    // Send Email to IT
    console.log("Ready to execute sendAccessRequestMail");
    await sendAccessRequestMail(selectedMemberRowData);

    // Email sent signal
    res.status(200).json(selectedMemberRowData);
  } catch (error) {
    console.error("Error retrieving data:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

router.post("/rejected-by-teamlead", async (req, res) => {
  try {
    const { selectedMembers } = req.body;
    console.log("selectedMembers: ", selectedMembers);

    const selectedMemberRowData = await accessRequestModel.findAll({
      where: {
        emailaddress: selectedMembers.map((member) => member.emailaddress),
      },
    });
    console.log("selectedMemberRowData: ", selectedMemberRowData);

    // Update teamleadapprove status for each member
    for (const member of selectedMemberRowData) {
      await member.update({ teamleadapprove: "REJECTED" });
    }

    // Email sent signal
    res.status(200).json(selectedMemberRowData);
  } catch (error) {
    console.error("Error retrieving data:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// GET: Switches the Status of a new member from pending to approved and add member to the team roster table
router.get("/approve-by-it", async (req, res) => {
  try {
    const { token } = req.query;
    // Token does not exist
    if (!token) {
      return res.status(400).json({ success: false, error: "Token Required" });
    }

    const accessRequest = await accessRequestModel.findOne({
      where: { token },
    });

    // Request Not Found on database
    if (!accessRequest) {
      return res
        .status(404)
        .json({ success: false, error: "Access Request Not Found" });
    }
    await accessRequest.update({ itapprove: "APPROVED" });

    return res.status(200).json({
      success: true,
      msg: `Successfully updated the status to APPROVED for New Member: 
      ${accessRequest.firstname} 
      ${accessRequest.lastname}`,
    });
  } catch (error) {
    console.error(error.message);
    return res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;
