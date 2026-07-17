/** FileStore：迷你编排域模块。 */
export class FileStore {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createFileStore = (data={}) => new FileStore(data);
