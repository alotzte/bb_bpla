const roundInt = (value: number) => Math.round(value);

const numberToLocale = (value: number) =>
  value.toLocaleString(undefined, { minimumFractionDigits: 2 });

export const formatNumber = {
  /** Окргуление до целого числа */
  roundInt,
  /** Отображение корректной суммы */
  numberToLocale,
};
