import torchSprite from '../assets/animated_torch.png';


const PixelTorch = () => {
  return (
    <div
      className="torch"
      style={{ backgroundImage: `url(${torchSprite})` }}
    />
  );
};

export default PixelTorch;
