import { useEffect, useState } from 'react';
import { Button, Form, Modal } from 'react-bootstrap';
import { Recipe, RecipeList } from '../types/interfaces';
import { recipeTypes, recipeTypeLabels } from '../types/constants';
import switchIcon from '../assets/switch_icon.svg';
import { getRecipes } from '../api/recipesApi';
import { Record } from 'react-bootstrap-icons';
import { updateMealPlanSchema } from '../api/apiSchemas/mealPlansSchemas';


interface Props {
    day: number;
    recipes: Record<string, Recipe>;
    show: boolean;
    handleClose: () => void;
    handleClick: (updateMealPlanData: updateMealPlanSchema) => void;
}

export function EditMealModal(
    {day, recipes, show, handleClose, handleClick}
    : Props) {
    const [editModes, setEditModes] = useState<Record<string, boolean>>(
        Object.fromEntries(
            Object.keys(recipes).map((recipeType) => [recipeType, false])
        ));
    const [mealRecipeIds, setMealRecipeIds] = useState<Record<string, number>>(
            Object.fromEntries(
            Object.keys(recipes).map(
                (recipeType) => [recipeTypes[recipeType], recipes[recipeType].id])));
    const [recipeLists, setRecipeLists] = useState<Record<string, RecipeList[]>>({});

    const getRecipeList = (recipeType: string) => {
        getRecipes({recipe_type: recipeTypes[recipeType]})
            .then((res) => {
                setRecipeLists(prevValues => ({
                    ...prevValues,
                    [recipeType]: res.data
                }));
            });
    }

    const handleSwitchClick = (recipeType: string) => {
        setEditModes({
            ...editModes,
            [recipeType]: !editModes[recipeType]
        });
    }

    const handleChange = (new_recipe_id: number, recipeType: string) => {
        setMealRecipeIds(prevValues => ({
            ...prevValues,
            [recipeTypes[recipeType]]: new_recipe_id
        }));
    }

    const handleSaveClick = () => {
        const meals: Record<number, Record<string, number>> = {
            [day]: mealRecipeIds
        };
        handleClick({meals});
    };

    useEffect(() => {
        Object.keys(recipes).map((recipeType) => {
            getRecipeList(recipeType);
        });
    }, []);

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
                            {`${recipeTypeLabels[recipeTypes[recipeType]]}:`}
                        </b>
                        { editModes[recipeType]? (
                            <Form.Select
                                aria-label="Select Recipe"
                                onChange={(e) => handleChange(Number(e.target.value), recipeType)}
                            >
                                <option value="" disabled>{recipes[recipeType].title}</option>
                                {recipeLists[recipeType]?.map((recipe) => (
                                    <option key={recipe.id} value={recipe.id}>
                                        {recipe.title}
                                    </option>
                                ))}
                            </Form.Select>
                        ) : (
                            <span>{recipes[recipeType].title}</span>
                        )}
                    </div>
                ))}
            </Modal.Body>
            <Modal.Footer>
                <Button
                    className="custom_button"
                    onClick={() => handleSaveClick()}
                >
                    {'Save'}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}
