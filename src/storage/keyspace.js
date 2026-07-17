/** Keyspace：迷你编排域模块。 */
export class Keyspace {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createKeyspace = (data={}) => new Keyspace(data);
