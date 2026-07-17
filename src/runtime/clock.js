/** Clock：迷你编排域模块。 */
export class Clock {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createClock = (data={}) => new Clock(data);
