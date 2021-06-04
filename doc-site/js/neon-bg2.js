
const synthwave = document.querySelector('.synthwave');

function updateRatios({ x, y, ...rest }) {
  const { offsetWidth, offsetHeight } = synthwave;

  const centerX = offsetWidth / 2;
  const centerY = offsetHeight / 2;

  const ratioX = (centerX - x) / centerX;
  const ratioY = (centerY - y) / centerY;
  
  document.documentElement.style.setProperty('--ratio-x', ratioX);
  document.documentElement.style.setProperty('--ratio-y', ratioY);
}

synthwave.addEventListener('mousemove', updateRatios, { passive: true })