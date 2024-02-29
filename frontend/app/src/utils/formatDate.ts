/**
 * Formats a date to "MMM DD" format.
 * @param {Date} date - The date object.
 * @returns {string} The formatted date string in "MMM DD" format.
 */
export function formatDate(date: Date): string {
    const monthStrings: string[] = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];
    return `${monthStrings[date.getMonth()]} ${date.getDate()}`;
}
