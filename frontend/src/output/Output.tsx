
const Output = ({text}: any) => {

    const handleExport = async () => {
        try {
          const response = await fetch("https://server-livid-delta-83.vercel.app/export-pdf", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
                text: text.simplified,
                company: text.company,
              }),
          });
      
          if (!response.ok) {
            throw new Error("Could not create PDF");
          }
      
          const blob = await response.blob();
      
          const url = window.URL.createObjectURL(blob);
      
          const link = document.createElement("a");
          link.href = url;
          link.download = `${text.company}-${new Date().toLocaleString("en-US", {
            month: "long",
            year: "numeric",
          })}.pdf`;
      
          document.body.appendChild(link);
          link.click();
      
          link.remove();
          window.URL.revokeObjectURL(url);
      
        } catch (error) {
          console.error(error);
          alert("Could not export PDF.");
        }
      };

  return (
    <div className="container">
        <div className="top">
            <div className="logo">Clarity</div>
            <div>We read between the lines so you don’t have to.</div>
        </div>

        <div className="middle t-center" >
            <div className="sub-logo" >The buzzwords are gone. Here’s what matters.</div>
            <br />
            <button className="main-btn" onClick={handleExport}>
                <div>
                    <div>Export PDF</div>
                    <div><svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="20px" fill="#FFFFFF"><path d="M480-100 213.08-366.92l41.77-42.77L450-214.54v-285.84h60v286.23l195.15-194.54 41.77 41.77L480-100Zm-30-480.38v-120h60v120h-60Zm0-200v-80h60v80h-60Z"/></svg></div>
                </div>
            </button>
        </div>
    </div>
  )
}

export default Output