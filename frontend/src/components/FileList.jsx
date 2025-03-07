const FileList = ({ files }) => {
    return (
      <div className="fileListDiv">
        
        <ol className="fileList">
          {files.map((file, index) => (
            <li key={index}>{file}</li>
          ))}
        </ol>
      </div>
    );
  };
  
  export default FileList;
  