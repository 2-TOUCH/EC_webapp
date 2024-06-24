import React from "react";
import { DataGrid } from "@mui/x-data-grid";
// import { use } from '../../../server/routes/accessRequestRouter';

const AccessForm = () => {
  const [users, setUsers] = React.useState([]);

  React.useEffect(() => {
    const url = "http://localhost:5000/access-requests/all";
    fetch(url)
      .then((res) => res.json())
      .then((users) => {
        setUsers(users);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  const data = users.map((user) => ({
    id: user.id,
    firstname: user.firstname,
    lastname: user.lastname,
    emailaddress: user.emailaddress,
    subteam: user.subteam,
    teamleadapprove: user.teamleadapprove,
    itapprove: user.itapprove,
    isOnboardingSent: user.isOnboardingSent,
    PhotoWaiverSentID: user.PhotoWaiverSentID,
    isPhotoWaiverSigned: user.isPhotoWaiverSigned,
    UPASentID: user.UPASentID,
    isUPASigned: user.isUPASigned,
    isOnboardingComplete: user.isOnboardingComplete,
  }));

  const columns = [
    { field: "firstname", headerName: "First Name", flex: 1 },
    { field: "lastname", headerName: "Last Name", flex: 1 },
    {
      field: "emailaddress",
      headerName: "Email Address",
      minWidth: 200,
      flex: 1,
    },
    { field: "subteam", headerName: "Sub Team", flex: 1 },
    { field: "teamleadapprove", headerName: "Team Lead", flex: 1 },
    { field: "itapprove", headerName: "IT Dept.", flex: 1 },
    { field: "isOnboardingSent", headerName: "Welcome Email Sent?", flex: 1} ,
    { field: "PhotoWaiverSentID", headerName: "Photo Waiver ID", flex: 1 },
    { field: "isPhotoWaiverSigned", headerName: "Photo Waiver Signed?", flex: 1 },
    { field: "UPASentID", headerName: "UPA ID", flex: 1 },
    { field: "isUPASigned", headerName: "UPA Signed?", flex: 1 },
    { field: "isOnboardingComplete", headerName: "Jira Account Created?", flex: 1 },
  ];

  const [rowSelectionModel, setRowSelectionModel] = React.useState([]);

  const handleSelectedRows = (newRowSelectionModel) => {
    setRowSelectionModel(newRowSelectionModel);
  };

  const handleSubmit = (event) => {
    event.preventDefault(); // won't refresh the page
    approveSubmit();
  };

  const handleReject = (event) => {
    event.preventDefault(); // won't refresh the page
    rejectSubmit();
  };

  const approveSubmit = async () => {
    console.log("Selected ID:", rowSelectionModel);
    const selectedRows = rowSelectionModel.map((selectedId) => {
      return data.find((row) => row.id === selectedId);
    });

    console.log("Selected Rows:", selectedRows);
    for (const row of selectedRows) {
      if (row.itapprove === "APPROVED") {
        window.alert(
          "At least one of the selected members has been approved by IT Dept!"
        );
      } else {
        try {
          const response = await fetch(
            "http://localhost:5000/access-requests/approved-by-teamlead",
            {
              method: "POST",
              body: JSON.stringify({ selectedMembers: selectedRows }),
              headers: {
                "Content-Type": "application/json",
              },
            }
          );
          const selectedMember = await response.json();
          console.log(selectedMember);
          if (response.status === 200) {
            window.alert(
              "Nice! Emails with final approval link will be sent to IT dept. to approve the selected member(s)!"
            );
            window.location.reload();
          }
        } catch (error) {
          console.error(error);
          window.alert("There is some error in this program.");
        }
      }
    }
  };

    const rejectSubmit = async () => {
        console.log('Selected ID:', rowSelectionModel);
        const selectedRows = rowSelectionModel.map((selectedId) => {
          return data.find((row) => row.id === selectedId);
        });
      
        console.log('Selected Rows:', selectedRows);
        for (const row of selectedRows) {
            if (row.itapprove === 'APPROVED') {
                window.alert("At least one of the selected members has been approved by IT Dept!")
            } else {
                try {
                    const response = await fetch('http://localhost:5000/access-requests/rejected-by-teamlead', {
                      method: 'POST',
                      body: JSON.stringify({ selectedMembers: selectedRows}),
                      headers: {
                        'Content-Type': 'application/json'
                      }
                    });
                    const selectedMember = await response.json();
                    console.log(selectedMember);
                    if (response.status === 200) {
                      window.alert("Rejected selected request(s)!")
                      window.location.reload()
                  }
                  } catch (error) {
                    console.error(error);
                    window.alert('There is some error in this program.');
                  }
            }
        }
      };

  return (
    <div className="content">
      <form>
        <h4>New Members' Requests</h4>
        <div style={{ height: 400, width: "100%" }}>
          <DataGrid
            rows={data}
            columns={columns}
            initialState={{
              pagination: {
                paginationModel: { page: 0, pageSize: 5 },
              },
            }}
            pageSizeOptions={[5, 10]}
            checkboxSelection
            onRowSelectionModelChange={handleSelectedRows}
            rowSelectionModel={rowSelectionModel}
          />
        </div>
        {/* <pre style={{ fontSize: 10 }}>
                    {JSON.stringify(rowSelectionModel, null, 4)}
                </pre> */}
        <div className="button-container">
          <button onClick={handleSubmit} className="submit-btn" type="submit">
            Approve!
          </button>
          <button onClick={handleReject} className="reject-btn" type="reject">
            Reject!
          </button>
        </div>
      </form>
    </div>
  );
};

export default AccessForm;
