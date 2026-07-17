/** Event：迷你编排域模块。 */
export class Event {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createEvent = (data={}) => new Event(data);
