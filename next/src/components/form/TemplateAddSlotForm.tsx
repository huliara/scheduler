import { Box } from "@mui/system";
import { TemplateAddSlotFields } from "../field/TemplateAddSlotFields";
import { TemplateSlot } from "@/types/TemplateType";
export const TemplateSlotForm = ({
  groupId,
  defaultValue,
  handleSubmit,
}: {
  groupId: string;
  defaultValue: TemplateSlot;
  handleSubmit: (data: TemplateSlot) => void;
}) => {
  const handleOnClick = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);

    handleSubmit({
      task_id: formData.get("task_id") as string,
      date_from_start: Number(formData.get("date_from_start")),
      start_time: formData.get("start_time") as string,
    });
  };

  return (
    <Box
      component="form"
      noValidate
      onSubmit={handleOnClick}
      sx={{ mt: 3, border: "1px solid #ccc", padding: 2, borderRadius: "8px" }}
      maxWidth={500}
    >
      {groupId ? (
        <TemplateAddSlotFields group_id={groupId} defaultValue={defaultValue} />
      ) : null}
    </Box>
  );
};
