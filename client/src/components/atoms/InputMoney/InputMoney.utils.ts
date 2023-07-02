const formatMoney = (value?: number) => {
	if (!value) return '0';

	if (value % 100 === 0) {
		return (value / 100).toFixed(0);
	}

	if (value % 10 === 0 && value > 100) {
		return (value / 100).toFixed(1);
	}

	return (value / 100).toFixed(2);
};

const parseMoney = (value?: string) => {
	if (!value) return 0;
	const numericValue = parseFloat(value);
	const intValue = Math.round(numericValue * 100);
	return isNaN(intValue) ? 0 : intValue;
};

export { formatMoney, parseMoney };
