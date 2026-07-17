/** EventBus：迷你编排域模块。 */
export class EventBus {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createEventBus = (data={}) => new EventBus(data);
