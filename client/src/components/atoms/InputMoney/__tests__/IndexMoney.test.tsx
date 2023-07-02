import { formatMoney, parseMoney } from '../InputMoney.utils';

describe('InputMoney utils', () => {
	const centsToDisplayed: Array<[number, string]> = [
		[12345, '123.45'],
		[123, '1.23'],
		[120, '1.2'],
		[100, '1'],
		[0, '0'],
	];

	it.each(centsToDisplayed)(
		'formats %p cents as %p',
		(cents: number, displayed: string) => {
			expect(formatMoney(cents)).toEqual(displayed);
		}
	);

	const displayedToCents = centsToDisplayed.map(
		([first, second]) => [second, first] as const
	);

	it.each(displayedToCents)(
		'parses %p as %p cents',
		(displayed: string, cents: number) => {
			expect(parseMoney(displayed)).toEqual(cents);
		}
	);
});
