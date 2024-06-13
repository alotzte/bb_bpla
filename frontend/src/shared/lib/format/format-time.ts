const msecToString = (msecs: number) => {
  const balanceMsecs = msecs % 1000;
  const secs = (msecs / 1000) % 60;
  let mins = Math.round(msecs / 60000);
  const hours = Math.floor(mins / 60);
  mins %= 60;

  return `${hours}:${mins < 10 ? `0${mins}` : mins}:${
    secs < 10 ? `0${secs}` : secs
  }.${balanceMsecs}`;
};

export const formatTime = {
  /** Перевод миллисекунд в часы */
  msecToString,
};
