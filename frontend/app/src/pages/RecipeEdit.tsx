import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { useState } from 'react';
import { FormCard } from '../components/FormCard';
import { RecipeForm } from '../components/RecipeForm';
import { RecipeIn } from '../api/apiSchemas/recipesSchemas';
import { updateRecipe, uploadImage } from '../api/recipesApi';
import { Container } from 'react-bootstrap';


interface RecipeEditState {
    recipe: RecipeIn;
}


interface Params {
    id: string;
    [key: string]: string;
}

export function RecipeEdit() {
    const { id = '' } = useParams<Params>();
    const location = useLocation();
    const navigate = useNavigate();
    const [recipe, setRecipe] = useState<RecipeIn>(
        (location.state as RecipeEditState).recipe);
    const [image, setImage] = useState<File | null>(null);

    function handleClick() {
        Promise.all([
            updateRecipe(id, recipe),
            image ? uploadImage(id, image) : Promise.resolve()
        ]).then(() => {
            console.log(image?.name);
            console.log(image?.size);
            navigate(`/recipes/${id}`);
        });
    }

    return (
        <Container className="pb-4">
            <FormCard
                title="Edit Recipe"
                formComponent={
                    <RecipeForm
                        recipe={recipe}
                        setRecipe={
                            (updatedRecipe: RecipeIn) => setRecipe(updatedRecipe)}
                        setImage={
                            (updatedImage: File | null) => setImage(updatedImage)}
                        withUrlField={false} />}
                buttonText="Save"
                handleClick={handleClick}
            />
        </Container>
    )
}
