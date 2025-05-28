import './Loader.css';

function Loader({ backdrop = false }) {
  const loaderElement = (
    <div className="loader">
      <div className="dot"></div>
      <div className="dot"></div>
      <div className="dot"></div>
    </div>
  );

  if (backdrop) {
    return (
      <div className="loader-backdrop">
        {loaderElement}
      </div>
    );
  }

  return loaderElement;
}

export default Loader;