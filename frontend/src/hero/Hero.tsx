import { useRef, useState } from "react";
import { ThreeDots } from 'react-loader-spinner'


const Hero = ({ onResult }: any) => {
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUpload = async (event: any) => {
    const file = event.target.files[0];

    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("https://clarity-ai-backend-seven.vercel.app/simplify", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Something went wrong");
      }

      const data = await response.json();

      onResult(data);
    } catch (error) {
      console.error(error);
      alert("Could not simplify the job description.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="top">
        <div className="logo">Clarity</div>
        <div>We read between the lines so you don’t have to.</div>
      </div>

      <div className="middle t-center">
        <div className="sub-logo">
          Upload a job description to uncover the real requirements, the role
          behind the buzzwords, and what the company is actually looking for.
        </div>

        <br />

        <input
          type="file"
          accept=".docx"
          ref={fileInputRef}
          onChange={handleUpload}
          style={{ display: "none" }}
        />

        <button
          className="main-btn"
          onClick={() => fileInputRef.current?.click()}
          disabled={loading}
        >
          <div>
            <div>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="24px"
                viewBox="0 -960 960 960"
                width="24px"
                fill="#FFFFFF"
              >
                <path d="M450-328.46v-336l-98.61 98.61-42.16-43.38L480-780l170.77 170.77-42.16 43.38L510-664.46v336h-60ZM252.31-180Q222-180 201-201q-21-21-21-51.31v-108.46h60v108.46q0 4.62 3.85 8.46 3.84 3.85 8.46 3.85h455.38q4.62 0 8.46-3.85 3.85-3.84 3.85-8.46v-108.46h60v108.46Q780-222 759-201q-21 21-51.31 21H252.31Z" />
              </svg>
            </div>

            <div>
            Upload Job Description
            </div>
          </div>
        </button>
      </div>

      

      {loading && (
  <>
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(128, 128, 128, 0.5)',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)',
        zIndex: 1,
      }}
    />

    <ThreeDots
      height="80"
      width="80"
      radius="9"
      color="#0d0d0d"
      ariaLabel="three-dots-loading"
      wrapperStyle={{
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        zIndex: 2,
      }}
      visible={true}
    />
  </>
)}
    </div>
  );
};

export default Hero;