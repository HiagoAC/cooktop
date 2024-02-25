import { expect, test } from 'vitest';
import { formatDate } from '../dateUtils';


test('formatDate function formats date correctly', () => {
    const date = new Date('2022-02-25');
    const expected = 'Feb 25';
    expect(formatDate(date)).toBe(expected);
});
