# turtle_regulation_FyFalina_Gokhool

## Installation
Pour installer ce package, dans le dossier source de votre catkin workspace faire un clone du package:
On supposera que votre catkin workspace s'appelle [Votre_nom]_ws et se situe dans votre home, remplacer par le bon chemin suivant l'oragnisation de vos dossiers.

```sh
cd [Votre_Nom]_ws/src
git clone https://github.com/fyfalina/turtle_regulation_FyFalina_Gokhool.git
```

Puis compiler et sourcer le setup.bash
```sh
catkin build
source ~/[Votre_nom]_ws/devel/setup.bash
```
# Utilisation

### Avec rosrun
Dans un terminal lancer le serveur ROS
```sh
roscore
```

Dans un second terminal, lancer le simulateur le turtlesim

```sh
rosrun turtlesim turtlesim_node
```

Dans un troisieme terminal 
```sh
source ~/[Votre_nom]_ws/devel/setup.bash
rosrun turtle_regulation_FyFalina_Gokhool set_way_point.py /cmd_vel:=/turtle1/cmd_vel /pose:=/turtle1/pose _kp:=[Valeur Constante]
```
En fonction de la valeur de kp, la tortue se tournera vers le waypoint a une vitesse constante. Pour des kp forts, la tortue pivotera rapidement. Pour des kp faibles, la tortue pivotera lentemant. Les kp ne doivent pas etre ni trop fort ni trop faibles.
