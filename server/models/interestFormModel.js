// const sequelize = require('../database')
// const {DataTypes} = require('sequelize')

// const interestForm = sequelize.define(
//     'InterestForm', 
//     {
//         email: {
//             type: DataTypes.STRING,
//             allowNull: false, 
//             validate: {
//                 isEmail: {
//                     msg: 'Invalid email address'
//                 },
//             },
//         },
//         fullname: {
//             type: DataTypes.STRING,
//             allowNull: false
//         },
//         sub_team: {
//             type: DataTypes.STRING,
//             allowNull: false
//         },
//     },
//     {
//         tableName: 'InterestForm',
//     }
// );

// module.exports = interestForm;