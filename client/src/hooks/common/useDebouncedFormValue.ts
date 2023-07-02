import { NamePath } from "rc-field-form/es/interface";
import { Form, FormInstance } from "antd";
import { useCallback, useEffect, useState } from "react";
import { debounce } from "lodash";

export const useDebouncedFormValue = <T>(
  dependencies: NamePath,
  form: FormInstance
) => {
  const [debouncedValue, setDebouncedValue] = useState<T>();
  const eagerValue = Form.useWatch(dependencies, form) as T;

  useEffect(() => {
    handleEagerValueChange(eagerValue);
  }, [eagerValue]);

  const handleEagerValueChange = useCallback(
    debounce((eagerValue: T) => setDebouncedValue(eagerValue), 250),
    [setDebouncedValue]
  );

  return debouncedValue;
};
