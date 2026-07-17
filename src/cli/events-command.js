/** EventsCommand：迷你编排域模块。 */
export class EventsCommand {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createEventsCommand = (data={}) => new EventsCommand(data);
