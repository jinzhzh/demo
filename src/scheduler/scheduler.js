/** Scheduler：迷你编排域模块。 */
export class Scheduler {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createScheduler = (data={}) => new Scheduler(data);
