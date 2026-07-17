/** MemoryStore：迷你编排域模块。 */
export class MemoryStore {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createMemoryStore = (data={}) => new MemoryStore(data);
