import { useState } from "react";
import {
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  TextField,
} from "@mui/material";
import ClearIcon from "@mui/icons-material/Clear";
import AddIcon from "@mui/icons-material/Add";
export const MultiTextField = ({
  state,
  onAdd,
  onDelete,
}: {
  state: string[];
  onAdd: (newValue: string) => void;
  onDelete: (index: number) => void;
}) => {
  return (
    <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      <AddTextField onAdd={onAdd} />
      {state.map((value, index) => {
        const labelId = `checkbox-list-label-${index}`;
        return (
          <ListItem
            key={index}
            secondaryAction={
              <IconButton aria-label="delete" onClick={() => onDelete(index)}>
                <ClearIcon />
              </IconButton>
            }
          >
            <ListItemText id={labelId} primary={`${index + 1}. ${value}`} />
          </ListItem>
        );
      })}
    </List>
  );
};

const AddTextField = ({ onAdd }: { onAdd: (newValue: string) => void }) => {
  const [text, setText] = useState("");
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value);
  };
  return (
    <ListItem>
      <ListItemIcon>
        <IconButton
          onClick={() => {
            onAdd(text);
            setText("");
          }}
        >
          <AddIcon />
        </IconButton>
      </ListItemIcon>
      <ListItemText>
        <TextField onChange={handleChange} fullWidth />
      </ListItemText>
    </ListItem>
  );
};
