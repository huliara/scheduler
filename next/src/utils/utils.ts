import axios from "@/axios";
import { GroupDataType } from "@/types/Base";

export const getGroupIds = (data: GroupDataType[]) =>
  Array.from(new Set(data.map((data) => data.group_id)));

export const handleOnClickDelete = (
  data_name: string,
  id: string,
  mutate: any
) => {
  axios
    .delete(`/${data_name}/${id}`)
    .then((res) => {
      mutate();
    })
    .catch((err) => {});
};
export const pick = <T extends object, K extends keyof T>(
  obj: T,
  keys: K[]
): Pick<T, K> => {
  const result = {} as Pick<T, K>;

  keys.forEach((key) => {
    result[key] = obj[key];
  });

  return result;
};
