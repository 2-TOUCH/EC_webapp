import React, { useState, useEffect } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const InterestForm = () => {

  const [formData, setFormData] = useState({
    emailaddress: '',
    firstname: '',
    lastname: '',
    subteam: '',
  });

  useEffect(() => {
      let _user = JSON.parse(sessionStorage.getItem('user_info'));
      
      if (_user){
        setFormData(prev => ({
          ...prev,
          emailaddress: _user.emailaddress,
          firstname: _user.firstname,
          lastname: _user.lastname,
        }))
      }
  }, []);

  

  const [errorBox, setErrorBox] = useState({
    subteam: false,
  });

  const [errorMessageS, setErrorMessageS] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const toggleErrorBox = (key, value) => {
    setErrorBox((prevErrorBox) => ({
      ...prevErrorBox,
      [key]: value,
    }));
  };

  const sendFormData = async () => {
    console.log(formData);
    try {
      const response = await fetch('http://localhost:5000/interest-form', {
        method: 'POST',
        body: JSON.stringify(formData),
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      console.log(data);
      if (response.status === 200) {
        window.alert(`${formData.firstname} ${formData.lastname} is added to the list successfully.`);
      } else {
        window.alert('Please check that the values are in the right format.');
      }
    } catch (error) {
      console.error(error);
      window.alert('There is an error in this program.');
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // const inputs = event.target.elements;
    // const ucdRegex = /^[a-zA-Z0-9._%+-]+@(ucdavis\.edu)$/i;

    let isFormValid = true;

    // setErrorMessageE(''); // Reset the error message

    Object.keys(formData).forEach((key, i) => {
      if (formData[key] === '') {
        toggleErrorBox(key, true);
        isFormValid = false;
        if(key === 'subteam'){
          setErrorMessageS(`The ${key} field cannot be left empty. Please enter a valid input.`);
        }// } else if (key === 'fullname'){
        //   setErrorMessageF(`The ${key} field cannot be left empty. Please enter a valid input.`);
        // } else if (key === 'emailaddress'){
        //   setErrorMessageE(`The ${key} field cannot be left empty. Please enter a valid input.`);
        // }
      // } else if (inputs[i].type === 'emailaddress') {
      //   if (ucdRegex.test(formData[key])) {
      //     toggleErrorBox(key, false);
      //   } else {
      //     toggleErrorBox(key, true);
      //     isFormValid = false;
      //     setErrorMessageE('Please enter a valid "UC Davis emailaddress address".');
      //   }
      } else {
        toggleErrorBox(key, false);
      }
    });

    isFormValid && sendFormData();
  };

  const mailto = (emailaddress) => {
    return <a href={`mailto:${emailaddress}`}>{emailaddress}</a>;
  };

  return (
    <div className="content">
      <div className="form">
        <form onSubmit={handleSubmit}>
          <h4>ECOCAR UC Davis Interest Form</h4>
          {/* <div className="input">
            <label htmlFor="emailaddress">Email</label>
            <input
              id="emailaddress"
              type="emailaddress"
              name="emailaddress"
              placeholder="Enter Your Email Address"
              onChange={handleChange}
              value={formData.emailaddress}
              className={errorBox.emailaddress ? 'errorStyle' : ''}
            />
            {errorBox.emailaddress && <span className="error" >{errorMessageE}</span>}
          </div>
          <div className="input">
            <label htmlFor="fullname">Full Name</label>
            <input
              id="fullname"
              type="text"
              name="fullname"
              placeholder="Enter New Member's Full Name"
              onChange={handleChange}
              value={formData.fullname}
              className={errorBox.fullname ? 'errorStyle' : ''}
            />
            {errorBox.fullname && <span className="error">{errorMessageF}</span>}
          </div> */}
          <div className="input">
            <label htmlFor="subteam">Sub Team</label>
            <select
              id="subteam"
              name="subteam"
              onChange={handleChange}
              value={formData.subteam}
              className={errorBox.subteam ? 'errorStyle' : ''}
            >
              <option value="">Select Sub Team (see description below) </option>
              <option value="CAV">CAV</option>
              <option value="DEI">DEI</option>
              <option value="PCM">PCM</option>
              <option value="PM">PM</option>
              <option value="SDI">SDI</option>
              {/* <option value='HMI/UX'>HMI/UX</option> */}
              <option value="Communications">Communications</option>
              {/* <option value='System Safety'>System Safety</option> */}
            </select>
            {errorBox.subteam && <span className="error">{errorMessageS}</span>}
          </div>
          <button className="submit-btn" type="submit">
            Request!
          </button>
          <div className="subteam-description">
            <h4>Subteam Descriptions</h4>
              <div>
              <Accordion>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel1a-content"
                  id="panel1a-header"
                >
                  <Typography>CAV</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography>
                    <strong>CAVS Sub-Team</strong> (Autonomous Stack - Software/Firmware) - <br />
                    <line style={{ textDecoration: 'underline' }}>Lead</line>: Hugo Michielsen Cerdan (
                    {mailto('ecocar-cav@ucdavis.edu')}) <br />
                    This is the software team that will largely be focused on implementing the autonomous stack in the vehicle
                    to allow the car to drive itself. The team will run drive scenario simulations, sensor integrations, and
                    perform tasks to develop a cohesive algorithm and platform that is at the core of the car's tech stack.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              <Accordion>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel2a-content"
                  id="panel2a-header"
                >
                  <Typography>DEI</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography>
                    <strong>Diversity, Equity, and Inclusion Sub-team</strong> (Stakeholder and Transportation research to inform
                    features and development plans) - <br />
                    <line style={{ textDecoration: 'underline' }}>Lead</line>: Vincent Colas (
                    {mailto('ecocar-dei@ucdavis.edu')}) <br />
                    The DEI team will conduct research and partner with various community organizations/stakeholders to introduce
                    programs to improve the landscape of DEI within the community. The DEI team's output will directly translate
                    to outreach events, policy recommendations, and even technical modifications to our vehicle!
                  </Typography>
                </AccordionDetails>
              </Accordion>
              <Accordion>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel2a-content"
                  id="panel2a-header"
                >
                  <Typography>PCM</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography>
                    <strong>PCM Sub-Team</strong> (System Dynamics and Controls) - <br />
                    <line style={{ textDecoration: 'underline' }}>Lead</line>: Abhigyan Majumdar (
                    {mailto('ecocar-pcm@ucdavis.edu')}) <br />
                    The PCM team deals with high-level powertrain architecture design, system modeling and controls development,
                    using MATLAB/Simulink. The team will improve vehicle performance (acceleration, handling, ride quality,
                    efficiency, etc) by implementing intelligent control systems.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              <Accordion>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel2a-content"
                  id="panel2a-header"
                >
                  <Typography>PM</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography>
                    <strong>Project Management Sub-Team</strong> (Organization, Process Engineering, Leadership) - <br />
                    <line style={{ textDecoration: 'underline' }}>Lead</line>: Ajay Suresh (
                    {mailto('ecocar-pm@ucdavis.edu')}) <br />
                    If you're interested in pursuing management related careers, this is the team to be a part of! The team
                    manages various aspects of the project and ensures that things are running smoothly and on schedule. There is
                    also a "Software Projects" sub-team that will be focused on making innovative process improvements using data
                    and automation tools.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              <Accordion>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel2a-content"
                  id="panel2a-header"
                >
                  <Typography>SDI</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography>
                    <strong>SDI Sub-Team</strong> (Hardware/Schematic/CAD) - <br />
                    <line style={{ textDecoration: 'underline' }}>Lead</line>: Nathaniel Lim (
                    {mailto('ecocar-sdi@ucdavis.edu')}) <br />
                    The SDI team makes dreams a reality and deals with physical implementation (mechanical, electrical, and
                    thermal) of simulated systems! A majority of the team will comprise of Electrical and Mechanical Engineers
                    who will aim to design and integrate the systems we create onto the vehicle. All CAD and CAE will be the
                    responsibility of the SDI team.
                  </Typography>
                </AccordionDetails>
              </Accordion>
              <Accordion>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls="panel2a-content"
                  id="panel2a-header"
                >
                  <Typography>Communications</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography>
                    <strong>Communications Sub-Team</strong> (Outreach, Social Media Initiatives, and Public Relations) - <br />
                    <line style={{ textDecoration: 'underline' }}>Lead</line>: Lauren Taylor (
                    {mailto('ecocar-comm@ucdavis.edu')}) <br />
                    If you'd also like to learn about outreach, public relations and communications, this is the meeting to
                    attend! The communications team is in charge of community outreach and social media activity that promotes
                    our goals to improve transportation inequity and be an effective grassroots workforce development program.
                  </Typography>
                </AccordionDetails>
              </Accordion>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default InterestForm;
