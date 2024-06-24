const Sequelize = require("sequelize");
require("dotenv").config();

// Create a Sequelize instance for the creation of a database
const sequelize = new Sequelize(
  process.env.DB_NAME,
  process.env.DB_USER,
  process.env.DB_PASSWORD,
  {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    dialect: "postgres",
    dialectOptions: {
      ssl: false,
    },
  },
);

module.exports = sequelize;
