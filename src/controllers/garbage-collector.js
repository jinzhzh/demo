/** GarbageCollector：迷你编排域模块。 */
export class GarbageCollector {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createGarbageCollector = (data={}) => new GarbageCollector(data);
