import { useState } from 'react';
import { Button, Form, Modal } from 'react-bootstrap';
import { Recipe, recipeTypeLabels } from '../data/recipe_detail';
import switchIcon from '../assets/switch_icon.svg';


interface Props {
    recipes: Record<string, Recipe>;
    show: boolean;
    handleClose: () => void;
    handleClick: () => void;
}

export function EditMealModal(
    {recipes, show, handleClose, handleClick}
    : Props) {
    const [editModes, setEditModes] = useState<Record<string, boolean>>(
        Object.fromEntries(
            Object.keys(recipes).map((recipeType) => [recipeType, false])
        ))
    const [editedValues, setEditedValues] = useState<Record<string, string>>(
            Object.fromEntries(
            Object.keys(recipes).map((recipeType) => [recipeType, ''])
        ))

    const handleSwitchClick = (recipeType: string) => {
        setEditModes({
            ...editModes,
            [recipeType]: !editModes[recipeType]
        });
    }

    const handleChange = (
        event: React.ChangeEvent<HTMLInputElement>,
        recipeType: string
        ) => {
        setEditedValues({
            ...editedValues,
            [recipeType]: event.target.value
        });
    }

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{'Change Recipes'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {Object.keys(recipes).map((recipeType) => (
                    <div key={recipeType} className="d-flex">
                        <Button
                            className="icon_button"
                            onClick={() => handleSwitchClick(recipeType)}
                            >
                            <img
                                src={switchIcon}
                                alt={`switch ${recipeType}`}
                                className="icon"
                            />
                        </Button>
                        <b className="me-2">
                            {`${recipeTypeLabels[recipeType]}:`}
                        </b>
                        { editModes[recipeType]? (
                            <Form.Control 
                                type="text"
                                value={editedValues[recipeType]}
                                onChange={(e) => handleChange(
                                    e as React.ChangeEvent<HTMLInputElement>,
                                    recipeType)}
                            />
                        ) : (
                            <span>{recipes[recipeType].title}</span>
                        )}
                    </div>
                ))}
            </Modal.Body>
            <Modal.Footer>
                <Button
                    className="custom_button"
                    onClick={handleClick}
                >
                    {'Save'}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}
