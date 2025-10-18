// @ts-check

// works as a JS script on this page (paste in console): https://bemaniwiki.com/?%A5%B3%A5%CA%A5%B9%A5%C6/SOUND+VOLTEX+EXCEED+GEAR/%B3%DA%B6%CA%A5%EA%A5%B9%A5%C8

/** @param {HTMLTableElement} table  */
function extractTableData(table) {
	const matrix = [...table.tBodies].flatMap((tbody) =>
		[...tbody.rows].map((row) =>
			[...row.cells].map((cell) => ({
				rowSpan: cell.rowSpan,
				colSpan: cell.colSpan,
				value: cell.textContent,
			})),
		),
	)

	for (let rowIndex = 0; rowIndex < matrix.length; rowIndex++) {
		const row = matrix[rowIndex]
		for (let colIndex = 0; colIndex < row.length; colIndex++) {
			const cell = row[colIndex]
			for (let colOffset = 1; colOffset < cell.colSpan; colOffset++) {
				row.push({ rowSpan: 1, colSpan: 1, value: cell.value })
			}
			cell.colSpan = 1

			for (let rowOffset = 1; rowOffset < cell.rowSpan; rowOffset++) {
				const rowAtOffset = matrix[rowIndex + rowOffset]
				if (rowAtOffset) {
					rowAtOffset.splice(colIndex, 0, {
						rowSpan: 1,
						colSpan: 1,
						value: cell.value,
					})
				}
			}
			cell.rowSpan = 1
		}
	}

	return matrix.map((row) => row.map((cell) => cell.value))
}

const baseSongs = extractTableData(
	/** @type {HTMLTableElement} */ (
		document.querySelector("#body > div:nth-child(18) > table")
	),
).map(([title, artist, bpm, nov, adv, exh, mxm]) => ({
	title,
	artist,
	bpm,
	nov,
	adv,
	exh,
	mxm,
}))

const memberSongs = extractTableData(
	/** @type {HTMLTableElement} */ (
		document.querySelector("#body > div:nth-child(21) > table")
	),
).map(([title, artist, bpm, nov, adv, exh, mxm]) => ({
	title,
	artist,
	bpm,
	nov,
	adv,
	exh,
	mxm,
}))

const blasterGateSongs = extractTableData(
	/** @type {HTMLTableElement} */ (
		document.querySelector("#body > div:nth-child(24) > table")
	),
).map(([title, artist, bpm, nov, adv, exh, mxm]) => ({
	title,
	artist,
	bpm,
	nov,
	adv,
	exh,
	mxm,
}))

const packSongs = extractTableData(
	/** @type {HTMLTableElement} */ (
		document.querySelector("#body > div:nth-child(27) > table")
	),
).map(([title, artist, bpm, nov, adv, exh, mxm, pack]) => ({
	title,
	artist,
	bpm,
	nov,
	adv,
	exh,
	mxm,
	pack,
}))

console.log({
	base: baseSongs,
	member: memberSongs,
	blasterGate: blasterGateSongs,
	pack: packSongs,
})
