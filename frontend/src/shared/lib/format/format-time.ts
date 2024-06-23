const msecToString = (msecs: number) => {
  const secs = Math.round((msecs / 1000) % 60);
  let mins = Math.round(msecs / 60000);
  const hours = Math.floor(mins / 60);
  mins %= 60;

  const currentMsecs = Math.round(msecs % 1000);

  return `${hours}:${mins < 10 ? `0${mins}` : mins}:${
    secs < 10 ? `0${secs}` : secs
  }.${currentMsecs}`;
};

export const formatTime = {
  /** Перевод миллисекунд в часы */
  msecToString,
};
