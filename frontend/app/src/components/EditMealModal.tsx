import { Button, Col, Modal, Row } from 'react-bootstrap';
import { Recipe } from '../data/recipe_detail';
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
                            >
                            <img
                                src={switchIcon}
                                alt={`switch ${recipeType}`}
                                className="icon"
                            />
                        </Button>
                        <p>{recipes[recipeType].title}</p>
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
