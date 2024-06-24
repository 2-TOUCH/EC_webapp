/* This code sets up an Express server with middleware to handle API requests. 
It connects to a database using Sequelize and defines routes for 
access requests, team roster details, and interest forms.
*/

const express = require("express");
const app = express();
require("dotenv").config();
const cors = require("cors");
const sequelize = require("./database");
const accessRequestRouter = require("./routes/accessRequestRouter");
const teamRosterRouter = require("./routes/teamRosterRouter");
const interestFormRouter = require("./routes/interestFormRouter");

// Middlewares
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors());

// API ROUTES
app.use("/access-requests", accessRequestRouter);
app.use("/member-detail", teamRosterRouter);
app.use("/interest-form", interestFormRouter);

const PORT = process.env.PORT || 5000;

// Sync the database using Sequelize, then start the server
sequelize
  .sync()
  .then((data) => {
    console.log("Database Connected");
    app.listen(PORT, () => {
      console.log(`Server running on PORT ${PORT}`);
    });
  })
  .catch((err) => {
    console.error("Error With Syncing the DB");
  });
